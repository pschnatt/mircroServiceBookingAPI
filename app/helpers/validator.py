import re

class Validator:

  @staticmethod
  def validateAmount(amount : int, limit : int) -> bool:
    return amount > limit