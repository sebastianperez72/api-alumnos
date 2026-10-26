import boto3

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    try:
        response = table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            ConditionExpression='attribute_exists(alumno_id)',  # solo si el alumno existe
            ReturnValues='ALL_OLD'
        )
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {
            'statusCode': 404,
            'mensaje': 'Alumno no existe'
        }
    # Salida (json)
    return {
        'statusCode': 200,
        'mensaje': 'Alumno eliminado',
        'alumno_eliminado': response['Attributes']
    }
