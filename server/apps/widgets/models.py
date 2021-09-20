from django.db import models


class Widget(models.Model):
    CRITERION_CHOICES = (
        ('gt', 'больше'),
        ('lt', 'меньше'),
    )
    VALIDITY_CHOICES = (
        ('1 day, 0:00:00', '1 день'),
        ('7 days, 0:00:00', '7 дней'),
        ('30 days, 0:00:00', '30 дней'),
    )
    owner = models.ForeignKey(to='users.User', on_delete=models.CASCADE,
                              verbose_name='Владелец', related_name='widgets')
    category = models.ForeignKey(to='budget.TransactionCategory', on_delete=models.CASCADE,
                                 verbose_name='Категория', related_name='widgets')
    money_limit = models.FloatField(verbose_name='Лимит суммы')
    validity = models.DurationField(verbose_name='Срок действия', choices=VALIDITY_CHOICES)
    criterion = models.CharField(max_length=2, choices=CRITERION_CHOICES, verbose_name='Критерий')
    color = models.CharField(max_length=7, verbose_name='Цвет (hex)')
    created_at = models.DateTimeField(verbose_name='Дата создания')

    def __str__(self):
        return '[{} {} на {}] создано: {}'.format(self.criterion, str(self.money_limit),
                                                  self.category, str(self.created_at))

    class Meta:
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'
