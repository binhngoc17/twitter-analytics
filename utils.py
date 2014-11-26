class NestedDict(object):
	__slots__ = ('_dict')

	def __init__(self, _dict=None):
		if _dict is None:
			self._dict = {}
		else:
			self._dict = _dict

	def __getstate__(self):
		return self._dict

	def __setstate__(self, state):
		self._dict = state

	def _get(self, key):
		parts = key.split('.')
		curr = self._dict

		for k in parts:
			curr = curr[k]

		return curr

	def _set(self, key, value):
		parts = key.split('.')
		curr = self._dict

		for k in parts[:-1]:
			if k in curr:
				curr = curr[k]
			else:
				empty = curr[k] = {}
				curr = empty

		curr[parts[-1]] = value

	def _del(self, key):
		parts = key.split('.')
		curr = self._dict

		for k in parts[:-1]:
			curr = curr[k]

		del curr[parts[-1]]

	def __len__(self):
		return len(self._dict)

	def __getitem__(self, key):
		return self._get(key)

	def __setitem__(self, key, value):
		self._set(key, value)

	def __delitem__(self, key):
		self._del(key)

	def __contains__(self, key):
		try:
			self._get(key)
			return True
		# pylint: disable=bare-except
		except:
			return False

	def get(self, key, default=None):
		try:
			return self._get(key)
		# pylint: disable=bare-except
		except:
			return default

	def pop(self, key, default=None):
		try:
			val = self._get(key)
			self._del(key)
			return val
		# pylint: disable=bare-except
		except:
			return default

	def update(self, E=None, **F):
		if E:
			if hasattr(E, 'keys') and callable(E.keys):
				for k in E:
					self._set(k, E[k])
			else:
				for (k, v) in E:
					self._set(k, v)
		for k in F:
			self._set(k, F[k])
			self[k] = F[k]

	def __getattr__(self, key):
		return getattr(self._dict, key)

	def __str__(self):
		return str(self._dict)

	def __repr__(self):
		return str(self)
