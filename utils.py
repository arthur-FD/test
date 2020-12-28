from datetime import date
def numberOfDays(y, m):
      leap = 0
      if y% 400 == 0:
         leap = 1
      elif y % 100 == 0:
         leap = 0
      elif y% 4 == 0:
         leap = 1
      if m==2:
         return 28 + leap
      list = [1,3,5,7,8,10,12]
      if m in list:
         return 31
      return 30

def get_last_day_quarter(quarter,year):
    if quarter==1:
        return(date(year,3,31))
    elif quarter==2:
        return(date(year,6,30))
    elif quarter==3:
        return(date(year, 9,30))
    elif quarter==4:
        return(date(year,12,31))
    else: return 'invalid input'

def find_col(year,months_available):
    return [col for col in months_available if str(year) in col]

