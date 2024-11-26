import React from "react";
import ListUsers from "../users/ListUsers";

const UserList: React.FC = () => {
    return (
        <div className="pt-4">
            <h3 className="text-base/7 font-semibold text-gray-900 text-center sm:text-left">
            Anmälda deltagare
            </h3>
            <ListUsers />
        </div>
    );
}

export default UserList;