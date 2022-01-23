using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PythonMovement : MonoBehaviour
{
    //everything needed for moving
    public CharacterController controller;
    Vector3 velocity; // x = right left, z = forward backward, y = up down
    Vector3 move;
    public float speed = 12f;
    public float gravity = -9.81f;
    public float movementSmoothness = 5f;
    public float verticalSpeed = 3f;
    public float rayLenght = 8f;

    //ground check stuff
    public Transform groundCheck;
    public float groundDistance = 0.4f;
    public LayerMask groundMask;

    public float angleMod = 4f;
    public float rotationSpeed = 0.1f;
    private float angle;

    // Update is called once per frame
    public float[] Movement(float angle = -1, float height = 0)
    {
        this.angle = angle;
        //Debug.Log("ANGLES: "+angle + " VS. " + this.transform.eulerAngles.y+angleMod);
        Rotation(angle);
        float x = 0;
        if(this.transform.eulerAngles.y <= angle+angleMod && this.transform.eulerAngles.y >= angle-angleMod && angle!=-1)
        {
            x = GetForward();
        }
        move = transform.forward * x;

        move = Vector3.Lerp(controller.transform.position, move, movementSmoothness); // smooth everything out 
        controller.Move(move * Time.deltaTime); // move * speed * deltaTime -> to make it independent from framerate
        //controller.Move(velocity * Time.deltaTime); // t^2 (time * time)
        velocity = Vector3.zero;

        Ray downRay = new Ray(controller.transform.position, -controller.transform.up);
        RaycastHit hitDown;
        
        if (height < transform.position.y)
        {
            velocity.y = verticalSpeed; //fly up
        }
        if (height > transform.position.y)
        {
            Debug.DrawRay(controller.transform.position, -controller.transform.up * 1f, Color.blue);
            if (Physics.Raycast(downRay, out hitDown, 1f) && !hitDown.collider.isTrigger)
            {
                velocity.y = 0;
            }
            else
            {
                velocity.y = -verticalSpeed; //fly down
            }
        }
        

        float[] positionArray = new float[] { transform.position.z, transform.position.x, transform.position.y};
        //Debug.Log(positionArray);
        return positionArray;
    }



    float GetForward()
    {
        float x = 1 * 0.5f * speed; // left right
        if (x > 0)
        {
            Ray horizontalRay = new Ray(controller.transform.position, controller.transform.right);
            Debug.DrawRay(controller.transform.position, controller.transform.right * rayLenght, Color.green);
            RaycastHit hit;
            if (Physics.Raycast(horizontalRay, out hit, rayLenght) && !hit.collider.isTrigger)
            {
                x = 0;
            }
        }
        else
        {
            Ray horizontalRay = new Ray(controller.transform.position, -controller.transform.right);
            Debug.DrawRay(controller.transform.position, -controller.transform.right * rayLenght, Color.green);
            RaycastHit hit;
            if (Physics.Raycast(horizontalRay, out hit, rayLenght) && !hit.collider.isTrigger)
            {
                x = 0;
            }
        }
        return x;
    }

    private void Rotation(float angle)
    {
        Quaternion currentRotation = transform.rotation;
        Quaternion toRotation =  Quaternion.Euler(0, angle,0);

        transform.rotation = Quaternion.Lerp(currentRotation, toRotation, Time.deltaTime);

    }

    private void OnDrawGizmosSelected()
    {
        Transform from = transform;
        Quaternion to = Quaternion.Euler(0, angle, 0);

        //controller.transform.rotation = Quaternion.Lerp(from.rotation, to, Time.deltaTime);

        Vector3 direction = to.eulerAngles;
        Gizmos.DrawRay(from.position, direction);
    }
}
