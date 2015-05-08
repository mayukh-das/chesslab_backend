import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'Hello'

class Greeting(messages.Message):
  message = messages.StringField(1)
  author = messages.StringField(2)


class GreetingCollection(messages.Message):
  items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
  Greeting(message='hello world!', author='andi'),
  Greeting(message='goodbye world!', author='kienle'),
])


@endpoints.api(name='myChessLab', version='01000',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])

class myChessLabApi(remote.Service):

  @endpoints.method(message_types.VoidMessage,
                    GreetingCollection,
                    path='hellogreeting2',
                    http_method='GET',
                    name='greetings2.listGreeting')
  
  def greetings_lixxst(self, unused_request):
    return STORED_GREETINGS

  ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,
      id=messages.IntegerField(1, variant=messages.Variant.INT32))

  @endpoints.method(ID_RESOURCE, Greeting,
                    path='hellogreeting/{id}', 
                    http_method='GET',
                    name='greetings.getGreeting')
                    
  def greeting_get(self, request):
    try:
      return STORED_GREETINGS.items[request.id]
    except (IndexError, TypeError):
      raise endpoints.NotFoundException('Greeting %s not found.' %
                                        (request.id,))

  @endpoints.method(message_types.VoidMessage, Greeting,
                    path='authed', http_method='POST',
                    name='greetings.authed')
  def greeting_authed(self, request):
    current_user = endpoints.get_current_user()
    email = (current_user.email() if current_user is not None
             else 'Anonymous')
    return Greeting(message='hello %s' % (email,))


  MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
      Greeting,
      times=messages.IntegerField(1, variant=messages.Variant.INT32, required=True))

  @endpoints.method(MULTIPLY_METHOD_RESOURCE,
                    Greeting,
                    path='hellogreeting/{times}',
                    http_method='POST',
                    name='greetings.multiply')
                    
  def greetings_multiply(self, request):
    return Greeting(message=request.message * request.times)





APPLICATION = endpoints.api_server([myChessLabApi])