# Architecture Overview

The platform includes user-service, notification-service, billing-service, analytics-service, and gateway-service.

notification-service consumes GET /users/{id} from user-service and reads the user_id field to enrich outbound notifications.

billing-service consumes GET /users/{id} from user-service and mainly uses id and email for invoice generation.

analytics-service reads user preferences for profile analytics dashboards.

gateway-service proxies selected user-service endpoints for external clients.
