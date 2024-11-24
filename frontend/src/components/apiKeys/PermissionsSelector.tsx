// src/components/apiKeys/PermissionsSelector.tsx

import React from 'react';

interface Permission {
  name: string;
  description: string;
}

interface PermissionsSelectorProps {
  availablePermissions: Permission[];
  selectedPermissions: string[];
  onChange: (permission: string) => void;
}

const PermissionsSelector: React.FC<PermissionsSelectorProps> = ({
  availablePermissions,
  selectedPermissions,
  onChange,
}) => {
  const groupedPermissions = availablePermissions.reduce<Record<string, Permission[]>>((groups, perm) => {
    const category = perm.name.split(':')[0]; // e.g., 'users', 'orders'
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(perm);
    return groups;
  }, {});

  return (
    <div>
      {Object.entries(groupedPermissions).map(([category, permissions]) => (
        <div key={category} className="mb-4">
          <h4 className="font-semibold capitalize">{category} Permissions:</h4>
          {permissions.map((permission) => (
            <label key={permission.name} className="flex items-center mb-2">
              <input
                type="checkbox"
                className="form-checkbox h-5 w-5 text-blue-600"
                checked={selectedPermissions.includes(permission.name)}
                onChange={() => onChange(permission.name)}
              />
              <span className="ml-2">
                <strong>{permission.name}</strong>: {permission.description}
              </span>
            </label>
          ))}
        </div>
      ))}
    </div>
  );
};

export default PermissionsSelector;
