from invoke import Collection
import watch

ns = Collection()
ns.add_collection(Collection.from_module(watch))
