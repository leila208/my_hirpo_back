from django.db import models
from account.utils import create_slug_shortcode
from django.contrib.auth import get_user, get_user_model
CompanyLeader = get_user_model()

skilltype=(
    ('Soft','Soft'),
    ('Hard','Hard'),
)

industries=(
    ('IT','IT'),
    ('Construction','Construction'),
)


class Skill(models.Model):
    name = models.CharField(max_length=255,verbose_name='Bacariq adi')
    skilltype = models.CharField(choices=skilltype,max_length=5,null=True,blank=True,verbose_name='Bacariq tipi')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Main SKill'
        verbose_name_plural = 'Main Skills'
        
        
class Department(models.Model):
    name = models.CharField(max_length=255,verbose_name='Department adi')
    description = models.TextField(verbose_name='Department haqqinda',null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Main Department'
        verbose_name_plural = 'Main Departments'
        

class Position(models.Model):
    name = models.CharField(max_length=20,verbose_name='Position adi')    
    description = models.TextField(verbose_name='Position haqqinda',null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Main Position'
        verbose_name_plural = 'Main Positions'
        

class DepartmentSkillNorm(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE,verbose_name='Skill for depnorm')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,verbose_name='Department for depnorm')
    position = models.ForeignKey(Position,on_delete=models.CASCADE,related_name='departmentskillnorm',verbose_name='Position for depnorm')
    norm = models.PositiveIntegerField(verbose_name='norm for depnorm')
    
    def __str__(self):
        return '-'
    
    class Meta:
        verbose_name = 'Main Skill norm'
        verbose_name_plural = 'Main Skill norms'
        
        
class Weight(models.Model):
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE,related_name='skill')
    weight = models.PositiveSmallIntegerField(verbose_name='Skill agirligi')
    
    def __str__(self):
        return str(self.weight)
    
    class Meta:
        verbose_name = 'Main Skill weight'
        verbose_name_plural = 'Main Skill weights'     