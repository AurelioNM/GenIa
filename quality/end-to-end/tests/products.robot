*** Settings ***
Resource    ../resources/common.robot
Resource   ../variables/env.robot

*** Test Cases ***
Should Create Product Successfully
    Create Product Session

    ${body}=    Create Dictionary
    ...    name=Pringles
    ...    description=Chips
    ...    price=4.50
    ...    category=SNACKS

    ${response}=    POST On Session
    ...    product
    ...    /v1/products
    ...    json=${body}

    Status Should Be    201    ${response}

    Should Be Equal As Strings    ${response.json()["name"]}    Pringles
    Should Be Equal As Strings    ${response.json()["category"]}    SNACKS