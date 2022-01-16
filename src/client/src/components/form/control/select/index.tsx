import React, { ReactElement } from 'react';
import { isThisTypeNode }      from 'typescript';
import { BasicComponentProps } from '../../../basic';


type SelectValue = string | number | readonly string[] | undefined;

export interface FormControlSelectProps<T extends SelectValue> extends BasicComponentProps
{
    name   ?: string;
    options : { title: string; value: T}[];
    value  ?: T;
    label  ?: string;
    id     ?: string;
    onChange?: ( value: T ) => void;
}


export default class FormControlSelect<T extends SelectValue> extends React.Component
{
    static count: number = 0;

    public id: string = '';
    public state: {
        value?: T
    } = {

    };

    constructor( readonly props: FormControlSelectProps<T> ) {
        super( props );

        FormControlSelect.count = FormControlSelect.count+1;

        this.id = `form-contorl-select-${FormControlSelect.count}`;
    }

    componentDidMount( )
    {
        const value = this.props.value;

        this.setState( { value } );
    }

    onChange( value: T ) : void
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
            <select 
                className={ "form-control " + this.props.className }
                id={id} 
                name={this.props.name}
                onChange={ event => this.onChange( event.target.value as T ) }
            >
                { 
                    this.props.options.map( ( elem, key ) => 
                        <option key={key} value={elem.value} selected={this.state.value === elem.value}>{elem.title}</option> )
                }
            </select>
            </div>
        );
    }
}