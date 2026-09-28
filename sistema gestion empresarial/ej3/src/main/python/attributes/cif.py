"""CIF attribute class"""
from attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class CIF(Attribute):
    """management of cif validation"""
    def __init__(self,cif_number:str):
        """init"""
        super().__init__()
        self._validation_pattern= r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$"
        self._error_message="Invalid CIF format"
        self._attr_value=self._validate(cif_number)

    def _validate(self, value):
        """validation algorithm"""
        super()._validate(value)
        head_letter = value[0]
        block_number = value[1:8]
        control_part = value[8]

        sum_even_position = 0
        sum_odd_position = 0

        for i in range(len(block_number)):
            if i % 2 == 0:
                number_found = int(block_number[i]) * 2
                if number_found > 9:
                    sum_even_position=sum_even_position + (number_found // 10) + (number_found % 10)
                else:
                    sum_even_position = sum_even_position + number_found
            else:
                sum_odd_position = sum_odd_position + int(block_number[i])

        total_sum = sum_even_position + sum_odd_position
        unit = total_sum % 10
        base_digit = 10 - unit

        if base_digit == 10:
            base_digit = 0

        control_character = "JABCDEFGHI"

        if head_letter in ('A', 'B', 'E', 'H'):
            if str(base_digit) != control_part:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif head_letter in ('P', 'Q', 'S', 'K'):
            if control_character[base_digit] != control_part:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return value
