// src/components/huntingYear/UserList.tsx

import React from "react";
import { User } from "../../types/HuntingYear";
import UserItem from "./UserItem";

interface UserListProps {
  users: User[] | null;
}

const UserList: React.FC<UserListProps> = ({ users }) => {
  if (!users || users.length === 0) {
    return <div>No users in this team for the selected hunting year.</div>;
  }

  return (
    <ul className="list-disc list-inside">
      {users.map((user) => (
        <UserItem key={user.id} user={user} />
      ))}
    </ul>
  );
};

export default UserList;
