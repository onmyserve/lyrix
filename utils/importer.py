import csv
import io
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type, Sequence, Tuple, Union
from django.db import models, transaction


@dataclass
class ImportResult:
    created: int = 0
    updated: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)
    total: int = 0

    @property
    def is_success(self) -> bool:
        return len(self.errors) == 0 and (self.created > 0 or self.updated > 0)


def normalize_header(header_name: str) -> str:
    """Normalizes header string for fuzzy matching (lowercase, no spaces/dashes/underscores)."""
    if not header_name:
        return ''
    return str(header_name).strip().lower().replace(' ', '').replace('_', '').replace('-', '')


def parse_csv_file(file_obj) -> List[Dict[str, str]]:
    """Parses a CSV file object into a list of row dictionaries."""
    content = file_obj.read()
    if isinstance(content, bytes):
        # Try UTF-8 with BOM, then UTF-8, then latin-1 fallback
        try:
            text = content.decode('utf-8-sig')
        except UnicodeDecodeError:
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                text = content.decode('latin-1')
    else:
        text = str(content)

    string_io = io.StringIO(text)
    reader = csv.DictReader(string_io)
    rows = []
    if reader.fieldnames:
        for row in reader:
            # Clean string keys & values
            clean_row = {
                (k.strip() if k else ''): (v.strip() if isinstance(v, str) else v)
                for k, v in row.items()
                if k is not None
            }
            # Ignore completely empty rows
            if any(clean_row.values()):
                rows.append(clean_row)
    return rows


def parse_excel_file(file_obj) -> List[Dict[str, str]]:
    """Parses an Excel file (.xlsx) object into a list of row dictionaries."""
    try:
        import openpyxl
    except ImportError as exc:
        raise ImportError("openpyxl is required to import Excel files. Please install openpyxl.") from exc

    wb = openpyxl.load_workbook(file_obj, data_only=True)
    sheet = wb.active

    rows_data = list(sheet.iter_rows(values_only=True))
    if not rows_data or len(rows_data) < 2:
        return []

    raw_headers = rows_data[0]
    headers = [str(h).strip() if h is not None else f"col_{i}" for i, h in enumerate(raw_headers)]

    parsed_rows = []
    for row_values in rows_data[1:]:
        if not any(v is not None and str(v).strip() != '' for v in row_values):
            continue  # Skip blank row

        row_dict = {}
        for header, val in zip(headers, row_values):
            if val is not None:
                row_dict[header] = str(val).strip()
            else:
                row_dict[header] = ''
        parsed_rows.append(row_dict)

    return parsed_rows


def parse_imported_file(file_obj, filename: str) -> List[Dict[str, str]]:
    """Automatically detects format (.csv or .xlsx) and parses row dictionaries."""
    filename_lower = filename.lower()
    if filename_lower.endswith('.csv'):
        return parse_csv_file(file_obj)
    elif filename_lower.endswith(('.xlsx', '.xls')):
        return parse_excel_file(file_obj)
    else:
        raise ValueError("Unsupported file format. Please upload a .csv or .xlsx file.")


class ModelFileImporter:
    """
    Generic reusable model importer.

    Usage example:
        importer = ModelFileImporter(
            model_class=Contact,
            field_mapping={
                'first_name': ['first_name', 'first name', 'fname', 'given name'],
                'last_name': ['last_name', 'last name', 'lname', 'surname'],
                'email': ['email', 'email address', 'e-mail'],
                'tag': ['tag', 'tags', 'group', 'type', 'category'],
            },
            required_fields=['first_name', 'email'],
            unique_key='email',
            update_existing=True,
        )
        result = importer.import_file(uploaded_file, uploaded_file.name)
    """

    def __init__(
        self,
        model_class: Type[models.Model],
        field_mapping: Dict[str, Sequence[str]],
        required_fields: Optional[Sequence[str]] = None,
        unique_key: Optional[str] = None,
        update_existing: bool = True,
        default_values: Optional[Dict[str, Any]] = None,
    ):
        self.model_class = model_class
        self.field_mapping = field_mapping
        self.required_fields = list(required_fields or [])
        self.unique_key = unique_key
        self.update_existing = update_existing
        self.default_values = default_values or {}

        # Pre-build normalized lookup map: normalized_alias -> model_field
        self._norm_alias_map: Dict[str, str] = {}
        for field_name, aliases in field_mapping.items():
            # Add field_name itself
            self._norm_alias_map[normalize_header(field_name)] = field_name
            for alias in aliases:
                self._norm_alias_map[normalize_header(alias)] = field_name

    def map_row_to_model_data(self, row_dict: Dict[str, str]) -> Dict[str, str]:
        """Maps incoming row dictionary keys to model field names based on field_mapping."""
        model_data = dict(self.default_values)
        for key, val in row_dict.items():
            norm_key = normalize_header(key)
            if norm_key in self._norm_alias_map:
                field_name = self._norm_alias_map[norm_key]
                model_data[field_name] = str(val).strip()
        return model_data

    def import_rows(self, raw_rows: List[Dict[str, str]]) -> ImportResult:
        """Processes list of row dicts and imports them into the model."""
        result = ImportResult(total=len(raw_rows))

        with transaction.atomic():
            for idx, raw_row in enumerate(raw_rows, start=1):
                row_data = self.map_row_to_model_data(raw_row)

                # Check required fields
                missing_fields = [
                    req_f for req_f in self.required_fields
                    if not row_data.get(req_f)
                ]
                if missing_fields:
                    result.errors.append(
                        f"Row {idx}: Missing required field(s): {', '.join(missing_fields)}"
                    )
                    result.skipped += 1
                    continue

                if self.unique_key:
                    unique_val = row_data.get(self.unique_key)
                    if not unique_val:
                        result.errors.append(f"Row {idx}: Unique key '{self.unique_key}' missing.")
                        result.skipped += 1
                        continue

                    # Search for existing record
                    lookup = {self.unique_key: unique_val}
                    existing = self.model_class.objects.filter(**lookup).first()

                    if existing:
                        if self.update_existing:
                            changed = False
                            for k, v in row_data.items():
                                if getattr(existing, k, None) != v:
                                    setattr(existing, k, v)
                                    changed = True
                            if changed:
                                existing.save()
                                result.updated += 1
                            else:
                                result.skipped += 1
                        else:
                            result.skipped += 1
                    else:
                        self.model_class.objects.create(**row_data)
                        result.created += 1
                else:
                    self.model_class.objects.create(**row_data)
                    result.created += 1

        return result

    def import_file(self, file_obj, filename: str) -> ImportResult:
        """Parses file and imports records into database."""
        try:
            raw_rows = parse_imported_file(file_obj, filename)
        except Exception as e:
            result = ImportResult()
            result.errors.append(f"File parsing error: {str(e)}")
            return result

        if not raw_rows:
            result = ImportResult()
            result.errors.append("The uploaded file is empty or has no data rows.")
            return result

        return self.import_rows(raw_rows)
