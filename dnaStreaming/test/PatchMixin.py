from mock import patch


class PatchMixin(object):
    """
    Testing utility mixin that provides methods to patch objects so that they
    will get unpatched automatically.
    """

    def patch_module(self, module, return_value=None):
        if str(getattr(module, '__class__')) == '<type \'instancemethod\'>':
            mock = self.patch_object(getattr(module, '__self__'), getattr(module, '__name__'))
        else:
            module_path = '{0}.{1}'.format(getattr(module, '__module__'), getattr(module, '__name__'))
            mock = self.patch(module_path)

        mock.return_value = return_value

        return mock

    def patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_object(self, *args, **kwargs):
        patcher = patch.object(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_dict(self, *args, **kwargs):
        patcher = patch.dict(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()
