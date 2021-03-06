# -*- coding: utf-8 -*-
from cadnano.assembly import Assembly
from cadnano.proxies.cnproxy import UndoCommand
from cadnano.part import Part
from cadnano.objectinstance import ObjectInstance
from cadnano.proxies.cnobject import CNObject

class RemoveInstanceCommand(UndoCommand):
    """
    Undo ready command for removing an instance.

    Args:
        cnobj:
        obj_instance: Object instance remove
    """

    def __init__(self,  cnobj: CNObject,
                        obj_instance: ObjectInstance):
        super(RemoveInstanceCommand, self).__init__("remove instance")
        self._items = (cnobj, cnobj.document(), obj_instance)
    # end def

    def redo(self):
        cnobj, doc, obji = self._items
        if cnobj._canRemove():
            if isinstance(cnobj, Part):
                cnobj.partRemovedSignal.emit(obji)
            else:
                cnobj.assemblyRemovedSignal.emit(obji)
        cnobj._decrementInstance(obji)
    # end def

    def undo(self):
        cnobj, doc, obji = self._items
        cnobj._incrementInstance(doc, obji)
        if cnobj._canReAdd():
            if isinstance(cnobj, Part):
                doc.documentPartAddedSignal.emit(doc, obji)
            elif isinstance(cnobj, Assembly):
                doc.documentAssemblyAddedSignal.emit(doc, obji)
            else:
                raise NotImplementedError
    # end def
# end class
