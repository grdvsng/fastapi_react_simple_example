import React, { ReactElement } from 'react';
import { isThisTypeNode }      from 'typescript';
import { BasicComponentProps } from '../../basic';


export interface FormRangeProps extends BasicComponentProps
{
    name   ?: string;
    value  ?: number;
    label  ?: string;
    id     ?: string;
    min    ?: number;
    max    ?: number;
    onChange?: ( value: number ) => void;
}


export default class FormRange extends React.Component
{
    static count: number = 0;

    public id: string = '';
    public state: {
        value?: number
    } = {

    };

    constructor( readonly props: FormRangeProps ) {
        super( props );

        FormRange.count = FormRange.count+1;

        this.id = `form-contorl-select-${FormRange.count}`;
    }

    componentDidMount( )
    {
        const value = this.props.value;

        this.setState( { value } );
    }

    onChange( value: number ) : void
    {
        this.setState( { value } );
                    
        if ( this.props.onChange )
        {
            this.props.onChange( value );
        }
    }

    render( ) : ReactElement
    {
        const id = this.props.id || this.id;

        return ( <div className="form-group">
            { this.props.label && <label htmlFor={id} className="form-label">{this.props.label}</label>}
            <input 
                type="range"
                className={ "form-range " + this.props.className }
                id={id} 
                name={this.props.name}
                onChange={ event => this.onChange( Number.parseInt( event.target.value ) ) }
                value={ this.state.value }
                min={this.props.min}
                max={this.props.max}
                
            >
            </input>
            <output>{this.state.value}</output>
            </div>
        );
    }
}