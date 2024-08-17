from typing import Annotated
from warehouse.core.db import get_db_session
from fastapi import Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

def verify_source(source):
    if source in ['customers','campaigns']:
        return source
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='source is customers or campaigns')
    
sourceDep = Annotated[str,Depends(verify_source)]

def query_parameters(offset:int | None=None,limit:int | None=None):
    query_parameters_dict ={}
    if offset:
        query_parameters_dict['offset'] = offset
    elif limit:
        query_parameters_dict['limit'] = limit
    return query_parameters_dict

queryDep = Annotated[dict|None,query_parameters]