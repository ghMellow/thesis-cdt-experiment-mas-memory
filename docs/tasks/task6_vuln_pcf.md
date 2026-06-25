# Task 6 — PCF: CORS Misconfiguration (DoS / Credential Leakage)

**ID:** task6_vuln_pcf  
**Tipo:** security_code_review  
**Difficoltà:** media  
**NF:** PCF (Policy Control Function)  
**CVE reference:** GHSA-98cp-84m9-q3qp

---

## Scenario

You are auditing the PCF (Policy Control Function) of a free5GC 5G core deployment. The PCF handles policy decisions for UEs: it manages AM (Access and Mobility) policies and determines what quality-of-service a UE is entitled to.

The handler below is called on every OAM GET request to retrieve a UE's AM policy. It sets CORS headers before delegating to the processor.

---

## Code Snippet

```go
// File: PCF/api_oam.go

package sbi

import (
    "net/http"

    "github.com/gin-contrib/cors"
    "github.com/gin-gonic/gin"

    "github.com/free5gc/openapi/models"
    "github.com/free5gc/pcf/internal/util"
    "github.com/free5gc/util/metrics/sbi"
)

const (
    CorsConfigMaxAge = 86400
)

func (s *Server) setCorsHeader(c *gin.Context) {
    // TODO: 1. turn these values into configurable variables
    // TODO: 2. use the official cors middleware
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
    s.setCorsHeader(c)   // ← called on every request

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

func (s *Server) getOamRoutes() []Route {
    return []Route{
        {
            Method:  http.MethodGet,
            Pattern: "/am-policy/:supi",
            APIFunc: s.HTTPOAMGetAmPolicy,
        },
    }
}
```

---

## Question

You are a 5G core security analyst. Analyze the `setCorsHeader` function and its usage and answer:

1. **Identify all security issues** in `setCorsHeader`. There is more than one. Describe each one precisely.
2. **Explain the DoS vector**: how can an attacker exploit the way `s.router.Use(...)` is called to cause a Denial of Service? What happens to the gin router's middleware chain over time?
3. **Explain the credential leakage risk**: why is the combination of `AllowAllOrigins: true` and `AllowCredentials: true` dangerous, and how does it violate the CORS specification?
4. **Propose a corrected version** of `setCorsHeader` (or the initialization pattern) that eliminates both the DoS vector and the credential risk.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "issues": [
    {
      "name": "short issue name",
      "description": "technical explanation"
    }
  ],
  "dos_vector": "explanation of the middleware chain growth DoS",
  "credential_risk": "explanation of AllowAllOrigins + AllowCredentials combination",
  "fix": "corrected code snippet or description of correct initialization pattern",
  "reasoning": "step-by-step analysis",
  "confidence": 0.0
}
```
