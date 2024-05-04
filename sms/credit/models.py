from django.db import models

import datetime

class Credit(models.Model):
    loan_amount = models.FloatField(db_column='LoanAmount')
    term_months = models.IntegerField(db_column='LoanTermMonths')
    annual_interest_rate = models.FloatField(db_column='AnnualInterestRate')
    penalty = models.FloatField(db_column='Penalty')
    date_received = models.DateField(default=datetime.date.today, db_column='DateReceived')
    
    class Meta:
        db_table = 'Credit'

    def __str__(self):
        return f"Loan ID: {self.pk}"










class PreCreditPayment(models.Model):
    payment_date = models.DateField(default=datetime.date.today,db_column='payment_date')
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2,db_column='principal_amount')
    interest = models.DecimalField(max_digits=10, decimal_places=2,db_column='interest')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,db_column='total_amount')
    days_overdue = models.IntegerField(db_column='days_overdue')
    penalty = models.DecimalField(max_digits=10, decimal_places=2,db_column='penalty')
    total = models.DecimalField(max_digits=10, decimal_places=2,db_column='total')
    balance = models.DecimalField(max_digits=10, decimal_places=2,db_column='balance')
    credit_id = models.IntegerField(db_column='credit_id')

    class Meta:
        db_table = 'TempCreditPayments'

    def __str__(self):
        return f"Payment ID: {self.pk}"
