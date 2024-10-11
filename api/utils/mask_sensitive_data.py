def mask_sensitive_data(value: str, mask_type: str = None) -> str:
    """
    Masks sensitive data such as phone numbers and names. If no mask_type is provided,
    it applies a default masking that hides most of the value.
    
    Args:
        value (str): The string to mask.
        mask_type (str, optional): The type of data ('phone' or 'name') to apply the appropriate masking rule.
                                   If not provided, a default masking will be applied.
    
    Returns:
        str: The masked string.
    """
    if mask_type == 'phone':
        # Mask all but the last 2 digits of the phone number
        return "****" + value[-2:] if len(value) > 2 else "****"
    elif mask_type == 'name':
        # Mask all but the first letter of the name
        return value[0] + "****" if len(value) > 1 else value
    else:
        # Default masking: Show only the first and last character, mask the rest
        return value[0] + "****" + value[-1] if len(value) > 2 else "****"