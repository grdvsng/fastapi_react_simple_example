import React, { ReactElement } from 'react';
import { isThisTypeNode }      from 'typescript';
import { BasicComponentProps } from '../basic';
import { GiRabbit }            from 'react-icons/gi';
import { RabbitColor, RabbitWeight } from '../../storage/types';


export interface RabbitProps extends BasicComponentProps
{
    weight  ?: RabbitWeight;
    weightPX?: number;
    color    : RabbitColor;
    animated?: boolean;
}


export default class RabbitIcon extends React.Component
{
    protected __weightPX?: number;

    constructor( readonly props: RabbitProps ) {
        super( props );
    }

    public get weightPX(  ) : number
    {
        const basicWeight = 5;

        if ( !this.__weightPX )
        {
            if ( !!this.props.weightPX )
            {
                this.__weightPX = this.props.weightPX;
            } else if ( this.props.weight ) {
                switch ( this.props.weight )
                {
                    case "thin"  : { this.__weightPX = basicWeight*2; break; }
                    case "normal": { this.__weightPX = basicWeight*4; break; }
                    case "plump" : { this.__weightPX = basicWeight*6; break; }
                }
            } else {
                this.__weightPX = basicWeight;
            }
        } 
        
        return this.__weightPX;
    }

    render( ) : ReactElement
    {
        
        return ( <span className={this.props.className}>
               <GiRabbit color={this.props.color} size={this.weightPX}/> 
            </span>
        );
    }
}