def split_full_name(full_name):
  given, family = full_name.split(' ')
  return given, family

def max_key(**maps):
  max_key, max_value = None, 0
  if not maps:
    return None
  
  for key, value in maps.items():
    if value > max_value:
      max_key, max_value = key, value
  
  return max_key