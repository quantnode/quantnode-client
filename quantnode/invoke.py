from serialize import deserialize, serialize
from actors import invoke_method
from dataproviders import ClientDataProvider
import helpers
import urllib


class RemoteInvocationHandler(object):

    def _invoke(self, repopath, method, cls, params):
        dp = ClientDataProvider()
        dp.reset_ack()

        usercls = helpers.find_implementation(repopath, cls)
        userobj = usercls(data_provider = dp)
        helpers.attach_parameters(dp, params)

        invoke_method(userobj, method, params)

        acks = dp.get_acks()
        s_acks = serialize(acks)
        s_acks = urllib.quote_plus(s_acks)
        return s_acks


    def _parse_params(self, data):
        params = deserialize(data, dotted=True)
        invocation = params.get('_invocation', {})
        method = invocation.get('method', '')
        cls = invocation.get('class', '')
        return method, cls, params


    def invoke(self, repopath, data):
        data = urllib.unquote_plus(data)
        method, cls, params = self._parse_params(data)

        try:
            if method == 'ping':
                return 'PONG'
            elif method == 'get_implementation_info':
                info = helpers.get_implementation_info(repopath)
                s_info = serialize(info)
                return s_info
            else:
                return self._invoke(repopath, method, cls, params)

        except Exception, e:
            info = {
                '__error__': helpers.get_error_info(e)
            }

            s_info = serialize(info)
            s_info = urllib.quote_plus(s_info)
            return s_info


