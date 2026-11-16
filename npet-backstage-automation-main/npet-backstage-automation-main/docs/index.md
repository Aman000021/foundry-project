# NPET Backstage Automation

Welcome to the NPET Backstage Automation documentation! This repository contains GitHub Actions workflows and PowerShell scripts for automating Backstage platform operations.

## Overview

This repository provides automation for:

- **Azure EntraID Group Management** - Create and manage Azure AD groups
- **Enterprise App Assignments** - Assign groups to Azure Enterprise Applications
- **SharedInfra Baseline** - Deploy baseline Azure infrastructure using Terraform
- **SonarQube Project Creation** - Automate SonarQube project setup
- **API Permissions Management** - Handle Azure API permission requests
- **ServiceNow Integration** - Update ServiceNow tickets programmatically
- **TechDocs Publishing** - Publish documentation to Azure Storage

## Available Workflows

### EntraID Group Management
- **File**: `.github/workflows/entra-id-group.yaml`
- **Purpose**: Create Azure AD security groups and assign owners
- **Scripts**: `.scripts/create-entra-id-group.ps1`, `.scripts/get-entra-group-id.ps1`

### Shared Infrastructure
- **File**: `.github/workflows/sharedinfra-baseline.yaml`
- **Purpose**: Deploy baseline Azure infrastructure including storage accounts, service principals, and networking
- **Integration**: Works with Terraform modules and Backstage catalog

### SonarQube Automation
- **File**: `.github/workflows/create-sonarqube-project.yaml`
- **Purpose**: Automate SonarQube project creation and GitHub secret configuration

## Getting Started

These workflows are designed to be called from Backstage templates or other automation systems. They use:

- **Azure Service Principal authentication** via OIDC
- **GitHub App tokens** for cross-repository operations
- **PowerShell scripts** for Azure operations
- **Terraform** for infrastructure provisioning

## Testing TechDocs

If you can see this documentation in Backstage under the **Docs** tab, then the TechDocs Azure Storage integration is working correctly!

## Next Steps

- Review individual workflow documentation
- Understand the PowerShell script parameters
- Check the Terraform modules integration
- Explore the Backstage catalog automation
