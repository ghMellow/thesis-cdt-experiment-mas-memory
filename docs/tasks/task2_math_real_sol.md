# Soluzione — Task 2 (math reale)

**ID:** task2_math_real_sol  
**Uso:** solo checker interno, MAI esposto all'agente

---

## Soluzione

Valori: 312.4, 298.7, 415.2, 389.6, 301.1

**Media:**
(312.4 + 298.7 + 415.2 + 389.6 + 301.1) / 5 = 1717.0 / 5 = **343.40**

**Deviazione standard campionaria (N-1):**
- diff²: (312.4-343.4)²=961.00, (298.7-343.4)²=1998.09, (415.2-343.4)²=5155.24, (389.6-343.4)²=2134.44, (301.1-343.4)²=1789.29
- Somma diff² = 12038.06
- Varianza campionaria = 12038.06 / 4 = 3009.515
- STD = √3009.515 = **54.86**

---

## Ground Truth

```json
{
  "answer": {
    "mean": 343.40,
    "std": 54.86
  },
  "type": "real",
  "tolerance": 0.5
}
```
