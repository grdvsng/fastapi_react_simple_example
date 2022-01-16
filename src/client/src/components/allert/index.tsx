import React from 'react';
import { BasicComponentProps } from '../basic';


export interface AllertProps extends BasicComponentProps
{
    type?: 'danger' | 'warning' | 'info' | 'primary';
    message?: string;
    hideAfter?: number;
}

export default class ComponentAllert extends React.Component
{
    state: {
        invisible?: boolean;
    } = { };
    
    props: AllertProps = { };

    constructor( props: AllertProps )
    {
        super(props);
    }

    componentDidMount()
    {
        setTimeout( () => this.setState( { invisible: true } ), this.props.hideAfter || 10000 );
    }

    render( ) : React.ReactElement
    {   
        if ( this.state.invisible )
        {
            return <></>;
        }

        return ( <div className={`alert alert-${this.props.type}`} role="alert">
            {this.props.message}
        </div> );
    }
}