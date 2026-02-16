"""Introspecção GraphQL completa da API Shopee Affiliate.

Gera documentação completa de todos os campos, argumentos e tipos.

Executa: python tests/full_introspection.py
"""
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from shopee_affiliate import ShopeeAffiliateClient
from dotenv import load_dotenv

load_dotenv()

# Introspecção completa do schema
FULL_INTROSPECTION = """
query FullIntrospection {
  __schema {
    queryType {
      name
      fields {
        name
        description
        args {
          name
          description
          defaultValue
          type {
            name
            kind
            ofType {
              name
              kind
              ofType {
                name
                kind
              }
            }
          }
        }
        type {
          name
          kind
          description
          fields {
            name
            description
            isDeprecated
            deprecationReason
            type {
              name
              kind
              ofType {
                name
                kind
                ofType {
                  name
                  kind
                  fields {
                    name
                    description
                    type {
                      name
                      kind
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    mutationType {
      name
      fields {
        name
        description
        args {
          name
          description
          type {
            name
            kind
          }
        }
        type {
          name
          kind
          fields {
            name
            type {
              name
            }
          }
        }
      }
    }
    types {
      name
      kind
      description
      fields {
        name
        description
        type {
          name
          kind
        }
      }
      enumValues {
        name
        description
      }
    }
  }
}
"""


def print_section(title: str, char: str = "="):
    """Imprime uma seção formatada."""
    print(f"\n{char * 70}")
    print(f"  {title}")
    print(f"{char * 70}\n")


def analyze_field(field: dict, indent: int = 0) -> dict:
    """Analisa um campo e retorna informações estruturadas."""
    info = {
        "name": field.get("name"),
        "description": field.get("description"),
        "args": [],
        "return_type": None,
        "return_fields": [],
    }

    # Analisar argumentos
    for arg in field.get("args", []):
        arg_info = {
            "name": arg.get("name"),
            "type": resolve_type(arg.get("type")),
            "description": arg.get("description"),
            "default": arg.get("defaultValue"),
        }
        info["args"].append(arg_info)

    # Analisar tipo de retorno
    return_type = field.get("type")
    info["return_type"] = resolve_type(return_type)

    # Se for OBJECT, analisar os campos
    if return_type and return_type.get("kind") == "OBJECT":
        for f in return_type.get("fields", []):
            field_info = {
                "name": f.get("name"),
                "type": resolve_type(f.get("type")),
                "description": f.get("description"),
                "deprecated": f.get("isDeprecated", False),
            }
            info["return_fields"].append(field_info)

    return info


def resolve_type(type_obj: dict) -> str:
    """Resolve o nome do tipo GraphQL."""
    if not type_obj:
        return "Unknown"

    kind = type_obj.get("kind")

    if kind == "NON_NULL":
        return resolve_type(type_obj.get("ofType")) + "!"
    elif kind == "LIST":
        return f"[{resolve_type(type_obj.get('ofType'))}]"
    else:
        return type_obj.get("name", "Unknown")


def generate_markdown_doc(data: dict) -> str:
    """Gera documentação Markdown completa."""
    lines = []

    lines.append("# API Shopee Affiliate - Introspecção Completa\n")
    lines.append("> Documentação gerada automaticamente via introspecção GraphQL\n")

    schema = data.get("data", {}).get("__schema", {})

    # === QUERIES ===
    print_section("QUERIES", "=")
    lines.append("## Queries\n\n")

    query_type = schema.get("queryType", {})
    fields = query_type.get("fields", [])

    # Ordenar campos alfabeticamente
    fields.sort(key=lambda x: x["name"])

    for field in fields:
        field_name = field["name"]
        lines.append(f"### {field_name}\n\n")

        desc = field.get("description")
        if desc:
            lines.append(f"{desc}\n\n")

        # Argumentos
        args = field.get("args", [])
        if args:
            lines.append("**Argumentos:**\n\n")
            lines.append("| Argumento | Tipo | Descrição |\n")
            lines.append("|-----------|------|-----------|\n")

            for arg in args:
                arg_name = arg.get("name")
                arg_type = resolve_type(arg.get("type"))
                arg_desc = arg.get("description", "-")
                lines.append(f"| {arg_name} | `{arg_type}` | {arg_desc} |\n")

            lines.append("\n")

        # Tipo de retorno
        return_type = field.get("type")
        if return_type:
            lines.append(f"**Retorna:** `{resolve_type(return_type)}`\n\n")

        # Campos do retorno (se for OBJECT)
        if return_type and return_type.get("kind") == "OBJECT":
            return_fields = return_type.get("fields", [])
            if return_fields:
                lines.append("**Campos:**\n\n")
                for f in return_fields:
                    f_name = f.get("name")
                    f_type = resolve_type(f.get("type"))
                    f_desc = f.get("description", "")
                    deprecated = " ⚠️ *Deprecated*" if f.get("isDeprecated") else ""
                    lines.append(f"- `{f_name}`: `{f_type}` - {f_desc}{deprecated}\n")
                lines.append("\n")

        lines.append("---\n\n")

    # === MUTATIONS ===
    print_section("MUTATIONS", "=")
    lines.append("## Mutations\n\n")

    mutation_type = schema.get("mutationType", {})
    if mutation_type:
        mutation_fields = mutation_type.get("fields", [])

        for field in mutation_fields:
            field_name = field["name"]
            lines.append(f"### {field_name}\n\n")

            desc = field.get("description")
            if desc:
                lines.append(f"{desc}\n\n")

            # Argumentos
            args = field.get("args", [])
            if args:
                lines.append("**Argumentos:**\n\n")
                lines.append("| Argumento | Tipo | Descrição |\n")
                lines.append("|-----------|------|-----------|\n")

                for arg in args:
                    arg_name = arg.get("name")
                    arg_type = resolve_type(arg.get("type"))
                    arg_desc = arg.get("description", "-")
                    lines.append(f"| {arg_name} | `{arg_type}` | {arg_desc} |\n")

                lines.append("\n")

            lines.append("**Retorna:**\n\n")
            return_type = field.get("type")
            if return_type and return_type.get("fields"):
                for f in return_type.get("fields", []):
                    lines.append(f"- `{f.get('name')}`: `{resolve_type(f.get('type'))}`\n")
            lines.append("\n")

            lines.append("---\n\n")

    # === TIPOS ===
    print_section("TIPOS E ENUMS", "=")
    lines.append("## Tipos e Enums\n\n")

    types = schema.get("types", [])
    enum_types = [t for t in types if t.get("kind") == "ENUM"]

    # Enums
    if enum_types:
        for enum_type in enum_types:
            name = enum_type.get("name")
            desc = enum_type.get("description", "")
            lines.append(f"### Enum: {name}\n\n")
            if desc:
                lines.append(f"{desc}\n\n")

            lines.append("| Valor | Descrição |\n")
            lines.append("|-------|-----------|\n")
            for val in enum_type.get("enumValues", []):
                v_name = val.get("name")
                v_desc = val.get("description", "-")
                lines.append(f"| `{v_name}` | {v_desc} |\n")
            lines.append("\n")

    return "".join(lines)


def run_full_introspection():
    """Executa introspecção completa e gera documentação."""
    client = ShopeeAffiliateClient(
        app_id=os.getenv("SHOPEE_APP_ID", ""),
        app_secret=os.getenv("SHOPEE_APP_SECRET", ""),
    )

    print_section("INTROSPECÇÃO COMPLETA - API SHOPEE AFFILIATE")

    print("Enviando query de introspecção...")
    result = client._request(FULL_INTROSPECTION)

    # Salvar JSON bruto
    output_dir = Path("docs")
    output_dir.mkdir(exist_ok=True)

    json_path = output_dir / "introspection_raw.json"
    print(f"\nSalvando JSON bruto: {json_path}")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Gerar Markdown
    print("\nGerando documentação Markdown...")
    markdown = generate_markdown_doc(result)

    md_path = output_dir / "API_INTROSPECTION.md"
    print(f"Salvando Markdown: {md_path}")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print_section("CONCLUÍDO!")
    print(f"✓ JSON salvo em: {json_path}")
    print(f"✓ Markdown salvo em: {md_path}")

    # Análise rápida
    schema = result.get("data", {}).get("__schema", {})
    query_fields = schema.get("queryType", {}).get("fields", [])
    mutation_fields = schema.get("mutationType", {}).get("fields", [])

    print("\n📊 Resumo:")
    print(f"  • Queries: {len(query_fields)}")
    print(f"  • Mutations: {len(mutation_fields)}")

    # Listar todas as queries
    print("\n📋 Queries disponíveis:")
    for f in sorted(query_fields, key=lambda x: x["name"]):
        print(f"  - {f['name']}")

    # Listar todas as mutations
    if mutation_fields:
        print("\n📋 Mutations disponíveis:")
        for f in sorted(mutation_fields, key=lambda x: x["name"]):
            print(f"  - {f['name']}")

    return result


if __name__ == "__main__":
    run_full_introspection()
