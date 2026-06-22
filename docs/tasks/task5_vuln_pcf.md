# Task 5 — 5G Code Vulnerability Detection (PCF)

**ID:** task5_vuln_pcf  
**Tipo:** textual  
**Difficoltà:** media

---

## Scenario

The following Go source file is taken from the **PCF** (Policy Control Function) of
free5gc, an open-source 5G Core implementation. It is the SBI (Service Based
Interface) handler for the OAM AM-policy endpoint.

```go
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

Analyze the code and identify the **security vulnerability** it contains.
Explain the mechanism that triggers it and its impact, and point to the
function and line(s) responsible.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": {
    "vulnerabilities": [
      {
        "type": "short vulnerability class (e.g. DoS, injection, ...)",
        "location": "function and/or line reference",
        "severity": "low | medium | high | critical",
        "description": "what is wrong and why"
      }
    ]
  },
  "reasoning": "...",
  "confidence": 0.0
}
```
