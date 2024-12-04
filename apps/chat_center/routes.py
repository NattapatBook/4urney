from apps.chat_center.consumer import ChatConsumer,TestDataConsumer

routes=[  
    ('chat', ChatConsumer),
    ('test-data', TestDataConsumer)
    ]