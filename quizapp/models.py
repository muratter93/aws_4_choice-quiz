from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Question(models.Model):
    """ 問題モデル """
    CATEGORY_CHOICES = [
        ('unclassified', '未分類'),
        ('cloud_computing', 'クラウドコンピューティング'),
        ('on_premise', 'オンプレミス'),
        ('public_cloud', 'パブリッククラウド'),
        ('private_cloud', 'プライベートクラウド'),
        ('hybrid_cloud', 'ハイブリッドクラウド'),
        ('scalability', 'スケーラビリティ'),
        ('elasticity', '弾力性'),
        ('pay_as_you_go', '従量課金制'),
        ('shared_responsibility', '責任共有モデル'),
        ('aws_pricing_calculator', 'AWS Pricing Calculator'),
        ('aws_cost_explorer', 'AWS Cost Explorer'),
        ('ec2', 'EC2'),
        ('lambda', 'Lambda'),
        ('ecs', 'ECS'),
        ('eks', 'EKS'),
        ('fargate', 'Fargate'),
        ('s3', 'S3'),
        ('ebs', 'EBS'),
        ('efs', 'EFS'),
        ('s3_glacier', 'S3 Glacier'),
        ('storage_gateway', 'Storage Gateway'),
        ('rds', 'RDS'),
        ('dynamodb', 'DynamoDB'),
        ('aurora', 'Aurora'),
        ('redshift', 'Redshift'),
        ('elasti_cache', 'Amazon ElastiCache'),
        ('vpc', 'VPC'),
        ('cloudfront', 'CloudFront'),
        ('route_53', 'Route 53'),
        ('direct_connect', 'Direct Connect'),
        ('elastic_load_balancer', 'Elastic Load Balancer'),
        ('iam', 'IAM'),
        ('kms', 'KMS'),
        ('aws_shield', 'AWS Shield'),
        ('aws_waf', 'AWS WAF'),
        ('aws_organizations', 'AWS Organizations'),
        ('cloudwatch', 'CloudWatch'),
        ('cloudtrail', 'CloudTrail'),
        ('aws_config', 'AWS Config'),
        ('trusted_advisor', 'AWS Trusted Advisor'),
        ('auto_scaling', 'Auto Scaling'),
        ('transit_gateway', 'AWS Transit Gateway'),
        ('security_hub', 'AWS Security Hub'),
        ('systems_manager', 'AWS Systems Manager'),
        ('global_accelerator', 'AWS Global Accelerator'),
        ('aws_privatelink', 'AWS PrivateLink'),
    ]

    question_text = models.CharField(max_length=200)
    remarks = models.TextField(blank=True, null=True) 
    correct_answer = models.CharField(max_length=100)  
    explanation = models.TextField(blank=True, null=True)  
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='unclassified')

    def __str__(self):
        return f"[{self.get_category_display()}] {self.question_text}"


class Choice(models.Model):
    """ 選択肢モデル """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')  
    choice_text = models.CharField(max_length=100) 

    def __str__(self):
        return self.choice_text


class AnswerHistory(models.Model):
    """ 回答履歴モデル """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  
    is_correct = models.BooleanField() 
    answered_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.question.question_text} - {'⭕' if self.is_correct else '❌'}"


@receiver(post_save, sender=Question)
def create_default_choices(sender, instance, created, **kwargs):
    if created and instance.choices.count() == 0:
        default_choices = ["A", "B", "C", "D"]
        for choice_text in default_choices:
            Choice.objects.create(question=instance, choice_text=choice_text)
