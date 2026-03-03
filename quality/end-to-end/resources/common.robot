*** Settings ***
Library    RequestsLibrary
Resource   ../variables/env.robot


*** Keywords ***
Create Product Session
    Create Session    product    ${PRODUCT_BASE_URL}

Create Customer Session
    Create Session    customer    ${CUSTOMER_BASE_URL}

Create Chat Session
    Create Session    chat    ${CHAT_BASE_URL}

Create Order Session
    Create Session    order    ${ORDER_BASE_URL}

Execute Chat Interaction
    [Arguments]    ${session_id}    ${customer_email}    ${input}

    ${body}=    Create Dictionary
    ...    input=${input}
    ...    customer_email=${customer_email}

    ${headers}=    Create Dictionary
    ...    session-id=${session_id}

    ${response}=    POST On Session
    ...    chat
    ...    /v2/chat/interaction
    ...    json=${body}
    ...    headers=${headers}

    Log To Console    \nInteraction Input: ${input}
    Log To Console    Interaction Output:\n${response.json()}

    Status Should Be    200    ${response}

    RETURN    ${response}