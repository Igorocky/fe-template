open Expln_React_common
open Expln_React_render
open Expln_React_Mui
open Expln_React_Modal
open Expln_utils_promise

@react.component
let make = () => {
    let modalRef = useModalRef()
    let (msg, setMsg) = React.useState(() => "")

    let actSendReqToBe = () => {
        BE.method1({msg:msg})->hndRespErr(modalRef)->promiseMap(resp => {
            openInfoDialog(~modalRef, ~title="Response from the BE", ~text=resp.len->Belt_Int.toString, ())
        })->ignore
    }

    <Col>
        {"This is the root component."->React.string}
        <Row>
            <TextField
                size=#small
                style=ReactDOM.Style.make(~width="300px", ())
                label="Message"
                value=msg
                onChange=evt2str(str => setMsg(_ => str))
            />
            <Button onClick={_=>actSendReqToBe()}>
                {"Send"->React.string}
            </Button>
        </Row>
        <Expln_React_Modal modalRef />
    </Col>
    

}