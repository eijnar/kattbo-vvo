import React from "react";
import { User } from "../../types/HuntingYear";

interface UserItemProps {
  user: User;
}

const UserItem: React.FC<UserItemProps> = ({ user }) => {
  return (
    <li className="mb-1">
      <span className="font-medium">{user.name}</span> - {user.email}
    </li>
  );
};

export default UserItem;
