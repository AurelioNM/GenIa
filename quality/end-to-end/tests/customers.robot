*** Settings ***
Resource    ../resources/common.robot
Resource   ../variables/env.robot

*** Test Cases ***
Should Get Customer By Id
    Create Customer Session

    ${customer_id}=    Set Variable    01KJ3JT1MTS05R4ZQYRX0EMGG5

    ${response}=    GET On Session
    ...    customer
    ...    /v1/customers/${customer_id}

    Log To Console    Response batata: ${response.json()}

    Status Should Be    200    ${response}

    Should Be Equal As Strings    ${response.json()["id"]}    ${customer_id}
