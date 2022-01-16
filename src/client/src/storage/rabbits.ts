import { getRequest, postRequest } from './basic';
import { Rabbit, RabbitColor, RabbitWeight } from './types';


export default class Rabbits
{
    static rabbits: Rabbit[];

    static async generate( min: number=20, max: number=50, force: boolean=false ) : Promise<Rabbit[]>
    {
        if ( !this.rabbits || force )
        {
            this.rabbits = await getRequest( 'rabbit/generator/?', { min, max } );
        }

        return this.rabbits;
    }

    static async select( rabbits: Rabbit[], color: RabbitColor, weight: RabbitWeight, _limit: string|number ) : Promise<{
        selected: Rabbit[],
        remaining: Rabbit[]
    }>
    {
        const limit  = Number.parseInt( `${_limit}` );
        const params = {
            rabbits,
            "preferences": {
                "selection_paremeters": {
                  "limit": limit,
                  "order_by": "color"
                },
                color,
                weight
            }
        }

        return await postRequest( 'rabbit/select', params );
    }
}