import React, { useEffect, useState } from "react";
import { User } from "../../types/User";
import { fetchUsers } from "../../services/api/userService";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../catalyst/table";
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
    <Table>
      <TableHead>
        <TableRow>
          <TableHeader>Namn</TableHeader>
          <TableHeader>Roll</TableHeader>
          <TableHeader>Telefonnummer</TableHeader>
        </TableRow>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.id}>
            <TableCell>
            <div className="flex items-center gap-4">
                <div>
                  <div className="font-medium">{user.first_name} {user.last_name}</div>
                  <div className="text-zinc-500">
                    <a href="#" className="hover:text-zinc-700">
                      {user.email}
                    </a>
                  </div>
                </div>
              </div>
            </TableCell>
            <TableCell>Jaktledare</TableCell>
            <TableCell>{user.phone_number}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default ListUsers;
