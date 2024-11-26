import React from "react";
import { Heading } from "../catalyst/heading";

interface HeaderProps {
    title: string;
}


const Header: React.FC<HeaderProps> = ({title}) => {
    return (
        <div className="pb-5">
        <Heading>{title}</Heading>
        </div>
    );
}

export default Header;