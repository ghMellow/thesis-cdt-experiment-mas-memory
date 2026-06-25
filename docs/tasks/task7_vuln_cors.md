# Task 7 — Security Code Review: CORS Misconfiguration

**ID:** task7_vuln_cors
**Tipo:** textual
**Difficoltà:** alta

---

## Scenario

You are a 5G security engineer auditing the OAM (Operations, Administration and Maintenance) API of a PCF (Policy Control Function) network function. The endpoint `/am-policy/:supi` is used by internal management tools to retrieve AM policy data for a given UE.

The team has reported two symptoms:
1. Under sustained load, the PCF process memory grows steadily until the service crashes.
2. The OAM API is supposed to be accessible only from trusted internal tools, but the security team has flagged that its CORS configuration may be too permissive.

The relevant handler and helper function are the following:

```go
const CorsConfigMaxAge = 86400

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

For reference: `s.router` is the shared `*gin.Engine` instance used by this server. `cors.New(config)` returns a `gin.HandlerFunc`. `s.router.Use(handler)` appends a handler to the global middleware chain of the Gin engine.

---

## Question

Identify all security weaknesses and implementation bugs in the code above. For each issue, describe what causes it and what impact it has on the system or on the security posture of the endpoint.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": "description of all vulnerabilities and bugs found",
  "reasoning": "technical explanation for each issue, including root cause and impact",
  "confidence": 0.0
}
```
