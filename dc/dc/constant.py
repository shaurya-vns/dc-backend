RESPONSE_ERROR = 0
RESPONSE_SUCCESS = 1
RESPONSE_INVALID = 2

INVALID_TOKEN = 'Invalid token'

#Drill

ADDRESS_NOT_FOUND = 'Address not found'


PENDING = 1
ACTIVE = 2
PAUSED = 3
COMPLETED = 4
CANCELLED = 5
TRANSFERRED = 6
OPEN = 7
RESOLVED = 8
CLOSED = 9
PREPARING = 10
DELIVERED =  11
SKIPPED =12
WAITING =13
APPROVED =14
REJECTED =15
PAID = 16
PAYMENT_PENDING = 17
PAYMENT_RECEIVED = 18
PAYMENT_FAILED = 19
PAYMENT_REFUNDED = 20
 
 
STATUS_CHOICES = (
    (PENDING, "Pending"),
    (ACTIVE, "Active"),
    (PAUSED, "Paused"),
    (COMPLETED, "Completed"),
    (CANCELLED, "Cancelled"),
    (TRANSFERRED, "Transferred"),
    (OPEN, "Open"),
    (RESOLVED, "Resolved"),
    (CLOSED, "Closed"),
    (PREPARING, "Preparing"),
    (DELIVERED, "Delivered"),
    (SKIPPED, "Skipped"),
    (WAITING, "Waiting"),
    (APPROVED, "Approved"),
    (REJECTED, "Rejected"),
    (PAID, "Paid"),
    (PAYMENT_PENDING, "Payment Pending"),
    (PAYMENT_RECEIVED, "Payment Received"),
    (PAYMENT_FAILED, "Payment Failed"),
    (PAYMENT_REFUNDED, "Payment Refunded")
)