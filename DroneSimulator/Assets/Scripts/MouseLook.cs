using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseLook : MonoBehaviour
{
    public float mouseSensitivity = 100f;
    private float xRotation = 0f;
    public Camera playerCam;
    public Transform playerBody;

    // Start is called before the first frame update
    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked; //to not allow the cursor to exit the window!
        Cursor.visible = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (PauseMenuScript.isPaused)
        {
            Cursor.lockState = CursorLockMode.None;
            Cursor.lockState = CursorLockMode.Confined;
            Cursor.visible = true;
        }
        else
        {
            Cursor.lockState = CursorLockMode.None;
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
        }


        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity * Time.deltaTime; //Time.Delta Time-> Amount of time since last update -> no framerate dependence
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity * Time.deltaTime;

        xRotation -= mouseY; //amount of rotation

        playerBody.Rotate(Vector3.up * mouseX);
        xRotation = Mathf.Clamp(xRotation, -90f, 90f);

        playerCam.transform.localRotation = Quaternion.Euler(xRotation, 0f, 0f); //quaternion= Responsible for rotation in Unity, Euler Angle? (x, y, z) (because we also want to clamp
        //Debug.Log(Input.GetAxis("Mouse X") + " " + Input.GetAxis("Mouse Y"));

        
    }
}
