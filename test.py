import boto
from boto.s3.key import Key
from django.conf import settings
from photoshare import settings



from boto3.session import Session

AWS_ACCESS_KEY_ID = 'AKIA5RBCQVVKDZBQ6L7E'
AWS_SECRET_ACCESS_KEY = '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'

ACCESS_KEY='AKIA5RBCQVVKDZBQ6L7E'
SECRET_KEY='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'

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)
s3 = session.resource('s3')
your_bucket = s3.Bucket('image-storage-app')

for s3_file in your_bucket.objects.all():
    print(s3_file.key)

s3.Object('filestorageapp', 'th.jpeg').delete()    