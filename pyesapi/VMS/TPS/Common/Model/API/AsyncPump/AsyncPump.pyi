"""
Type stubs for VMS.TPS.Common.Model.API.AsyncPump
Generated from .NET XML documentation
"""

from typing import Any, List, Optional, Union, Dict, Iterable, overload
from datetime import datetime
from System import Array, Double, Single, Int32, Boolean, String
from System.Collections.Generic import KeyValuePair
from System import Collections

class SingleThreadSynchronizationContext:
    """
    Provides a SynchronizationContext object that is single-threaded.
    """
    def __init__(self) -> None: ...

    # Dispatches an asynchronous message to the synchronization context.
    def Post(self, d: Threading.SendOrPostCallback, state: Any) -> Any:
        """
        Args:
            d: The System.Threading.SendOrPostCallback delegate to call.
            state: The object passed to the delegate.
        """
        ...


    # Not supported.
    def Send(self, param1: Threading.SendOrPostCallback, param2: Any) -> Any:
        ...


    # Runs an loop to process all queued work items.
    def RunOnCurrentThread(self) -> Any:
        ...


    # Notifies the context that no more work will arrive.
    def Complete(self) -> Any:
        ...


    # Dispatches an asynchronous message to the synchronization context.
    def Post(self, d: Threading.SendOrPostCallback, state: Any) -> Any:
        """
        Args:
            d: The System.Threading.SendOrPostCallback delegate to call.
            state: The object passed to the delegate.
        """
        ...


    # Not supported.
    def Send(self, param1: Threading.SendOrPostCallback, param2: Any) -> Any:
        ...


    # Runs an loop to process all queued work items.
    def RunOnCurrentThread(self) -> Any:
        ...


    # Notifies the context that no more work will arrive.
    def Complete(self) -> Any:
        ...



class SingleThreadSynchronizationContextSetter:
    """
    Provides a temporary single-threaded environment until the diposal of this object (
    """
    # Sets SynchronizationContext to a
    @overload
    def __init__(self) -> None:
        ...


    # Sets SynchronizationContext to a
    @overload
    def __init__(self) -> None:
        ...


    # Resets the SynchronizationContext.
    def Dispose(self) -> Any:
        ...


    def Complete(self) -> Any:
        ...


    def Run(self) -> Any:
        ...


    # Resets the SynchronizationContext.
    def Dispose(self) -> Any:
        ...


    def Complete(self) -> Any:
        ...


    def Run(self) -> Any:
        ...



class SingleThreadSynchronizationContext:
    """
    Provides a SynchronizationContext object that is single-threaded.
    """
    def __init__(self) -> None: ...

    # Dispatches an asynchronous message to the synchronization context.
    def Post(self, d: Threading.SendOrPostCallback, state: Any) -> Any:
        """
        Args:
            d: The System.Threading.SendOrPostCallback delegate to call.
            state: The object passed to the delegate.
        """
        ...


    # Not supported.
    def Send(self, param1: Threading.SendOrPostCallback, param2: Any) -> Any:
        ...


    # Runs an loop to process all queued work items.
    def RunOnCurrentThread(self) -> Any:
        ...


    # Notifies the context that no more work will arrive.
    def Complete(self) -> Any:
        ...


    # Dispatches an asynchronous message to the synchronization context.
    def Post(self, d: Threading.SendOrPostCallback, state: Any) -> Any:
        """
        Args:
            d: The System.Threading.SendOrPostCallback delegate to call.
            state: The object passed to the delegate.
        """
        ...


    # Not supported.
    def Send(self, param1: Threading.SendOrPostCallback, param2: Any) -> Any:
        ...


    # Runs an loop to process all queued work items.
    def RunOnCurrentThread(self) -> Any:
        ...


    # Notifies the context that no more work will arrive.
    def Complete(self) -> Any:
        ...



class SingleThreadSynchronizationContextSetter:
    """
    Provides a temporary single-threaded environment until the diposal of this object (
    """
    # Sets SynchronizationContext to a
    @overload
    def __init__(self) -> None:
        ...


    # Sets SynchronizationContext to a
    @overload
    def __init__(self) -> None:
        ...


    # Resets the SynchronizationContext.
    def Dispose(self) -> Any:
        ...


    def Complete(self) -> Any:
        ...


    def Run(self) -> Any:
        ...


    # Resets the SynchronizationContext.
    def Dispose(self) -> Any:
        ...


    def Complete(self) -> Any:
        ...


    def Run(self) -> Any:
        ...



