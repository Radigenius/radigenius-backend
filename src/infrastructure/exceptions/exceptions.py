from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    success = False
    errors = None
    key = ""

    def __init__(self, detail, code, key="", errors=None):
        super().__init__(detail, code)
        self.status_code = code
        self.success = False
        self.key = key
        self.errors = errors


class EntityNotFoundException(BaseCustomException):
    def __init__(self, message="Entity Not Found!", key="not_found", errors=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, key=key, errors=errors)


class MultipleObjectsReturnedException(BaseCustomException):
    def __init__(
        self,
        message="Multiple Objects Returned!",
        key="multiple_objects_returned",
        errors=None,
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, key=key, errors=errors
        )


class EntityDeleteRestrictedException(BaseCustomException):
    def __init__(
        self,
        message="Entity Deletion Restricted!",
        key="delete_restricted",
        errors=None,
    ):
        super().__init__(message, status.HTTP_409_CONFLICT, key=key, errors=errors)


class EntityDeleteProtectedException(BaseCustomException):
    def __init__(
        self, message="Entity Deletion Protected!", key="delete_protected", errors=None
    ):
        super().__init__(message, status.HTTP_409_CONFLICT, key=key, errors=errors)


class CaptchaTokenInvalidException(BaseCustomException):
    def __init__(
        self,
        message="Captcha Token is Invalid!",
        key="captcha_token_invalid",
        errors=None,
    ):
        super().__init__(message, status.HTTP_403_FORBIDDEN, key=key, errors=errors)


class ValidationException(BaseCustomException):
    def __init__(
        self, message="Validation Error!", key="validation_error", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class InvalidTokenException(BaseCustomException):
    def __init__(self, message="Token is Invalid!", key="invalid_token", errors=None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, key=key, errors=errors)


class InvalidIdException(BaseCustomException):
    def __init__(self, message="id is Invalid!", key="invalid_id", errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class PasswordMissmatchException(BaseCustomException):
    def __init__(
        self, message="Password Missmatch!", key="password_missmatch", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class UserNotBannedException(BaseCustomException):
    def __init__(
        self, message="User is Not Banned", key="user_not_banned", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class UserIsNotActiveException(BaseCustomException):
    def __init__(
        self, message="User is Not Active", key="user_not_active", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class CastDtoException(BaseCustomException):
    def __init__(self, message="Cast Dto Error", key="cast_dto_error", errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class SMSException(BaseCustomException):
    def __init__(self, message="Send Sms Error", key="send_sms_error", errors=None):
        super().__init__(message, status.HTTP_502_BAD_GATEWAY, key=key, errors=errors)


class PasswordNotValidException(BaseCustomException):
    def __init__(
        self,
        message="Password is not valid",
        key="password_not_valid",
        errors=None,
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class InvalidOTPException(BaseCustomException):
    def __init__(
        self, message="OTP is not valid", key="otp_not_valid_or_expired", errors=None
    ):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, key=key, errors=errors)


class PaymentStartFailed(BaseCustomException):
    def __init__(
        self, message, key="payment_start_failed", code=status.HTTP_504_GATEWAY_TIMEOUT
    ):
        super().__init__(message, code=code, key=key, errors=[])


class PaymentVerificationFailed(BaseCustomException):
    def __init__(
        self,
        message,
        key="payment_verification_failed",
        code=status.HTTP_504_GATEWAY_TIMEOUT,
    ):
        super().__init__(message, code=code, key=key, errors=[])


class CouponInvalid(BaseCustomException):
    def __init__(
        self,
        key,
        message="Coupon is Not Valid!",
        code=status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, code=code, key=key, errors=[])


class ProductAvaiableStatusSentException(BaseCustomException):
    def __init__(
        self,
        message="Product Avaiable Already Sent!",
        key="product_avaiable_already_sent",
        code=status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, code=code, key=key, errors=[])


class UserBanException(BaseCustomException):
    def __init__(
        self,
        errors,
        message="User is Banned!",
        key="user_is_banned",
        code=status.HTTP_403_FORBIDDEN,
    ):
        super().__init__(message, code=code, key=key, errors=errors)


class UnsupportedFileTypeException(BaseCustomException):
    def __init__(
        self,
        file_type,
        errors=[],
        key="unsupported_file_type",
        code=status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(
            detail=f"{file_type} Is Not Supported", code=code, key=key, errors=errors
        )


class EntityAlreadyCreatedException(BaseCustomException):
    def __init__(
        self,
        entity_name,
        key="entity_already_created_exception",
        code=status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(
            detail=f"${entity_name} Already Created!", code=code, key=key, errors=[]
        )


class PermissionDeniedException(BaseCustomException):
    def __init__(self):
        super().__init__(
            detail="You do not have permission to perform this action.",
            code=status.HTTP_403_FORBIDDEN,
            key="permission_denied",
            errors=[],
        )


class NotAuthenticatedException(BaseCustomException):
    def __init__(self):
        super().__init__(
            detail="Authentication credentials were not provided.",
            code=status.HTTP_401_UNAUTHORIZED,
            key="not_authenticated",
            errors=[],
        )
