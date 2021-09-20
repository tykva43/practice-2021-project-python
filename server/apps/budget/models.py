from django.db import models


class Transaction(models.Model):
    owner = models.ForeignKey(to='users.User', on_delete=models.CASCADE,
                              verbose_name='Владелец', related_name='transactions')
    category = models.ForeignKey(to='TransactionCategory', on_delete=models.CASCADE,
                                 verbose_name='Категория', related_name='transactions')
    amount = models.FloatField(verbose_name='Сумма')
    date = models.DateField(verbose_name='Дата операции')

    def __str__(self):
        return '[{}] {}: {}'.format(str(self.owner_id), str(self.date), str(self.amount))

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class TransactionCategory(models.Model):
    CATEGORY_TYPES = (
        ('inc', 'Доход'),
        ('exp', 'Расход')
    )
    category_type = models.CharField(choices=CATEGORY_TYPES, max_length=3, verbose_name='Тип категории')
    name = models.CharField(max_length=100, verbose_name='Название категории')
    owner = models.ForeignKey(to='users.User', on_delete=models.CASCADE,
                              verbose_name='Владелец', related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Transaction category'
        verbose_name_plural = 'Transaction categories'
