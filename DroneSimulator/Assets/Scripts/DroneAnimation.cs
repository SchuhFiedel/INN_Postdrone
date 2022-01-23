using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DroneAnimation : MonoBehaviour
{

    //public CharacterController controller;
    Vector3 move;
    public Camera playerCam;
    public float movementSmoothness = 5f;
    public float rotationSpeed = 5f;
    public float maxAngle = 10f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        float x = Input.GetAxis("Horizontal")*(-maxAngle); 
        float z = Input.GetAxis("Vertical")* maxAngle; 

        //Debug.Log(transform.rotation.z + " Z"); // forward backward
        //Debug.Log(transform.rotation.y + " Y"); // mouse (but we are gonna put this on Q/E
        //Debug.Log(transform.rotation.x + " X"); // right left
        //Debug.Log(transform.eulerAngles); //x,y,z

        Quaternion fromRotation = transform.rotation; // get the angle that we are at currently
        Quaternion toRotation = Quaternion.Euler(z, playerCam.transform.eulerAngles.y, x);
        transform.rotation = Quaternion.Lerp(fromRotation, toRotation, rotationSpeed * Time.deltaTime);

        /*
        //Debug.Log(z + " =Z");
        if (z > 0) //rotate left for left movement
        {
            if (transform.eulerAngles.x < maxAngle || transform.eulerAngles.x > 300 - maxAngle)
            {
                transform.rotation = Quaternion.Lerp(transform.rotation, Quaternion.Euler(maxAngle, playerCam.transform.eulerAngles.y, transform.eulerAngles.z), rotationSpeed * Time.deltaTime);
                //transform.Rotate(Vector3.right, rotationSpeed);
                //Debug.Log(transform.eulerAngles);
            }
            
        }
        else if (z < 0) //rotate right for right movement
        {
            if (transform.eulerAngles.x < 180-maxAngle)
            {
                transform.rotation = Quaternion.Lerp(transform.rotation, Quaternion.Euler(300-maxAngle, playerCam.transform.eulerAngles.y, transform.eulerAngles.z), rotationSpeed * Time.deltaTime);
                //Debug.Log(transform.eulerAngles);
            }
        }
        else //rotate back to original posistion
        {
            transform.rotation = Quaternion.Lerp(transform.rotation, Quaternion.Euler(0, playerCam.transform.eulerAngles.y, transform.eulerAngles.z), rotationSpeed * Time.deltaTime);
            //Debug.Log(transform.eulerAngles);
        }

        //Debug.Log(x + " =X");
        if (x < 0) //rotate forward for forward movement
        {
            if (transform.eulerAngles.z < maxAngle || transform.eulerAngles.z > 300 - maxAngle)
            {
                transform.rotation = Quaternion.Lerp(transform.rotation, Quaternion.Euler(transform.eulerAngles.x, playerCam.transform.eulerAngles.y, maxAngle), rotationSpeed * Time.deltaTime);
                //Debug.Log(transform.eulerAngles);
            }
        }
        else if (x > 0) //rotate back for backwards movement
        {
            if (transform.eulerAngles.z < 180 - maxAngle)
            {
                transform.rotation = Quaternion.Lerp(transform.rotation, Quaternion.Euler(transform.eulerAngles.x, playerCam.transform.eulerAngles.y, 300 - maxAngle), rotationSpeed  * Time.deltaTime);
                //Debug.Log(transform.eulerAngles);
            }
        }
        else // rotate back to original position
        {
            transform.rotation = Quaternion.RotateTowards(transform.rotation, Quaternion.Euler(transform.eulerAngles.x, playerCam.transform.eulerAngles.y, 0), rotationSpeed * Time.deltaTime);
            //transform.rotation = Quaternion.Euler(transform.eulerAngles.x, playerCam.transform.eulerAngles.y, 0);
            //Debug.Log(transform.eulerAngles);
        }
        */
    }
}
