# Task 6 — Security Code Review: PCF CORS Misconfiguration (5G)

**ID:** task6_vuln_pcf
**Tipo:** security_code_review
**Difficoltà:** media
**NF:** PCF (Policy Control Function)

---

## Scenario

You are reviewing the OAM (Operations, Administration and Maintenance) API handler of the PCF (Policy Control Function) component of a free5GC 5G core network. The PCF exposes an HTTP endpoint that serves AM (Access and Mobility) policy data per subscriber (SUPI).

The function `setCorsHeader` is called at the beginning of each request to the OAM endpoint.

---

## Code Snippet

```go
const (
    CorsConfigMaxAge = 86400
)

func (s *Server) setCorsHeader(c *gin.Context) {
    s.router.Use(cors.New(cors.Config{
        AllowMethods: []string{"GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"},
        AllowHeaders: []string{
            "Origin", "Content-Length", "Content-Type", "User-Agent",
            "Referrer", "Host", "Token", "X-Requested-With",
        },
        ExposeHeaders:    []string{"Content-Length"},
        AllowCredentials: true,
        AllowAllOrigins:  true,
        MaxAge:           CorsConfigMaxAge,
    }))

    c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
    c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
    c.Writer.Header().Set(
        "Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, "+
            "X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
    c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, PATCH, DELETE")
}

func (s *Server) HTTPOAMGetAmPolicy(c *gin.Context) {
    s.setCorsHeader(c)

    supi := c.Params.ByName("supi")
    if supi == "" {
        problemDetails := &models.ProblemDetails{
            Title:  util.ERROR_INITIAL_PARAMETERS,
            Status: http.StatusBadRequest,
        }
        c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Title)
        c.JSON(int(problemDetails.Status), problemDetails)
        return
    }
    s.Processor().HandleOAMGetAmPolicyRequest(c, supi)
}
```

---

## Question

1. Identify the **security vulnerabilities** in the CORS configuration above (there may be more than one).
2. Explain the **concrete security or operational impact** in a 5G PCF deployment.
3. Propose a **corrected configuration**.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": {
    "vulnerabilities": ["vuln 1...", "vuln 2..."],
    "impact": "...",
    "fix": "..."
  },
  "reasoning": "...",
  "confidence": 0.0
}
```
