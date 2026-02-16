#!/usr/bin/env python3
"""Benchmark para comparar performance das implementações de _render()."""

import re
import timeit


def render_old(template: str, mapping: dict) -> str:
    """Implementação original usando str.replace() em loop."""
    out = template
    for key, value in mapping.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def render_new(template: str, mapping: dict) -> str:
    """Implementação otimizada usando re.sub()."""
    return re.sub(
        r'{{([a-zA-Z_][a-zA-Z0-9_]*)}}',
        lambda m: mapping.get(m.group(1), m.group(0)),
        template
    )


def benchmark():
    """Executa benchmark comparativo."""
    print("🧪 Validando saída idêntica...")

    # Template GraphQL REALISTA (com { } literais)
    template_real = """query {
  shopeeOfferV2(
    keyword: {{keyword}}
    sortType: {{sortType}}
    page: {{page}}
    limit: {{limit}}
  ) {
    nodes {
      itemId
      itemName
      itemPrice
    }
  }
}"""

    mapping = {
        "keyword": '"teste"',
        "sortType": "1",
        "page": "1",
        "limit": "10"
    }

    # Validar que ambas produzem mesma saída
    result_old = render_old(template_real, mapping)
    result_new = render_new(template_real, mapping)
    assert result_old == result_new, f"Saídas diferentes!\nOld: {result_old[:100]}...\nNew: {result_new[:100]}..."
    print("✅ Saída idêntica validada (template GraphQL real)\n")

    # Benchmark com template GraphQL real
    runs = 10000
    time_old = timeit.timeit(
        lambda: render_old(template_real, mapping),
        number=runs
    )
    time_new = timeit.timeit(
        lambda: render_new(template_real, mapping),
        number=runs
    )

    # Resultados - Cenário 1: Template pequeno (4 placeholders)
    print(f"📊 Resultados do Benchmark (template GraphQL pequeno, {runs:,} iterações):")
    print(f"   Implementação antiga: {time_old:.4f}s")
    print(f"   Implementação nova:   {time_new:.4f}s")
    speedup = time_old / time_new
    savings = (1 - time_new / time_old) * 100

    print(f"   Speedup:              {speedup:.2f}x")
    print(f"   Economia:             {time_old - time_new:.4f}s ({savings:.1f}%)")

    # Teste com mais placeholders (escala melhor)
    print("\n📈 Teste de escalabilidade (20 placeholders):")
    template_large = " ".join([f"{{field{i}}}" for i in range(20)])
    mapping_large = {f"field{i}": f"value{i}" for i in range(20)}

    time_old_large = timeit.timeit(
        lambda: render_old(template_large, mapping_large),
        number=runs
    )
    time_new_large = timeit.timeit(
        lambda: render_new(template_large, mapping_large),
        number=runs
    )

    print(f"   str.replace() loop: {time_old_large:.4f}s")
    print(f"   re.sub():          {time_new_large:.4f}s")
    speedup_large = time_old_large / time_new_large
    print(f"   Speedup:           {speedup_large:.2f}x mais rápido!")

    if speedup_large >= 3.0:
        print(f"   ✅ META ALCANÇADA: 3-5x mais rápido com muitos placeholders!")
    else:
        print(f"   ⚠️  Abaixo da meta (3-5x)")


if __name__ == "__main__":
    benchmark()
