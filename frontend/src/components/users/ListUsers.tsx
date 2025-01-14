// src/pages/ListUsers.tsx

import React, { useEffect, useState } from "react";
import { User } from "../../types/User";
import { fetchUsers } from "../../services/api/userService";
import Table, { Column } from "../common/Table";
import Spinner from "../common/Spinner";
import ErrorMessage from "../common/ErrorMessage";

const ListUsers: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getUsers = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await fetchUsers();
        setUsers(data);
      } catch (err: any) {
        setError(err.message || "An unexpected error occurred");
      } finally {
        setIsLoading(false);
      }
    };

    getUsers();
  }, []);

  const columns: Column<User>[] = [
    { header: "First Name", accessor: "first_name", sortable: true },
    { header: "Last Name", accessor: "last_name", sortable: true },
    { header: "Email", accessor: "email", sortable: true },
    { header: "Phone Number", accessor: "phone_number", sortable: false },
  ];

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner size="lg" color="text-blue-500" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto mt-8">
        <ErrorMessage message={error} />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto mt-8 p-4 bg-white shadow-md rounded">
      <h2 className="text-2xl font-semibold mb-4">User List</h2>
      <Table<User> data={users} columns={columns} className="overflow-x-auto" />
    </div>
  );
};

export default ListUsers;
