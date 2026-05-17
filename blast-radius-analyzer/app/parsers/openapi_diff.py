from app.domain.contracts import ContractChange


def extract_response_properties(document: dict, method: str, endpoint: str) -> dict[str, dict]:
    """Return response properties for an endpoint method."""
    operation = document.get("paths", {}).get(endpoint, {}).get(method.lower(), {})
    responses = operation.get("responses", {})
    success_response = responses.get("200", {})
    content = success_response.get("content", {}).get("application/json", {})
    schema = content.get("schema", {})
    return schema.get("properties", {})


def diff_openapi_response_fields(
    service_name: str,
    file_path: str,
    base_document: dict,
    head_document: dict,
) -> list[ContractChange]:
    """Return response field changes between two OpenAPI documents."""
    changes: list[ContractChange] = []
    base_paths = base_document.get("paths", {})
    head_paths = head_document.get("paths", {})
    shared_endpoints = sorted(set(base_paths) & set(head_paths))

    for endpoint in shared_endpoints:
        base_methods = base_paths.get(endpoint, {})
        head_methods = head_paths.get(endpoint, {})
        shared_methods = sorted(set(base_methods) & set(head_methods))

        for method in shared_methods:
            base_properties = extract_response_properties(base_document, method, endpoint)
            head_properties = extract_response_properties(head_document, method, endpoint)

            removed_fields = sorted(set(base_properties) - set(head_properties))
            for field_name in removed_fields:
                changes.append(
                    ContractChange(
                        service_name=service_name,
                        file_path=file_path,
                        method=method.upper(),
                        endpoint=endpoint,
                        change_type="field_removed",
                        field_path=field_name,
                        breaking=True,
                    )
                )

            shared_fields = sorted(set(base_properties) & set(head_properties))
            for field_name in shared_fields:
                base_type = base_properties.get(field_name, {}).get("type")
                head_type = head_properties.get(field_name, {}).get("type")
                if base_type != head_type:
                    changes.append(
                        ContractChange(
                            service_name=service_name,
                            file_path=file_path,
                            method=method.upper(),
                            endpoint=endpoint,
                            change_type="field_type_changed",
                            field_path=field_name,
                            breaking=True,
                        )
                    )

    return changes
