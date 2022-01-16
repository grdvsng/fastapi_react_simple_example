import urljoin       from 'url-join';
import { BASIC_URL } from './api.config';


class StorageAPIError extends Error 
{
    constructor( message: string, url: string='', method: string='GET' )
    {
        super( `-X ${method} '${url}' error='${message}'` );
    }
}


async function getRequestHandler<T>( _response: Promise<Response>, responseCode: number=200, url: string='' ) : Promise<T>
{
    try{
        const response = await _response;

        if ( response.status != responseCode )
        {
            throw new StorageAPIError( `invalide response status_code='${response.status}', waited='${response}'`, url, 'GET' )
        } else {
            return await response.json( );
        }
    } catch( error: unknown ) {
        throw new StorageAPIError( `${error}`, url, 'GET' );
    }
}

export async function getRequest<T>( prefix: string, filter: Record<string, any>, requestParams: RequestInit ={credentials: "include" }, responseCode: number=200 ) : Promise<T>
{
    const params = new URLSearchParams( filter );
    const url    = urljoin( BASIC_URL, prefix, params.toString( ) );

    requestParams.method = 'GET';

    return getRequestHandler( fetch( url, requestParams ), responseCode, url );
}

export async function postRequest<P extends object, T>(prefix: string, json: P, requestParams: RequestInit ={credentials: "include" }, responseCode: number=200 ) : Promise<T>
{
    const url = urljoin( BASIC_URL, prefix );
    
    requestParams.body    = JSON.stringify( json );
    requestParams.headers = new Headers( requestParams.headers || { } );

    requestParams.headers.set( 'Content-Type', 'application/json' );
    
    requestParams.method = 'POST';

    return getRequestHandler( fetch( url, requestParams ), responseCode, url );
}